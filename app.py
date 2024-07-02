from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api, Resource
from marshmallow import fields, validate, ValidationError
from models import Author, Book

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        from models import Author, Book

        api = Api(app, version='1.0', title='API Biblioteca', description='API para gerenciamento de autores e livros')

        class AuthorsSchema(ma.SQLAlchemyAutoSchema):
            class Meta:
                model = Author

            id = fields.Int(dump_only=True)
            name = fields.Str(required=True, error_messages={'required': 'O nome é obrigatório'})
            last_name = fields.Str(required=True, error_messages={'required': 'O sobrenome é obrigatório'})
            birth_date = fields.Date(required=True, error_messages={'required': 'A data de nascimento é obrigatória', 'type': 'Data de nascimento inválida'})
            nationality = fields.Str(required=True, error_messages={'required': 'A nacionalidade é obrigatória'})

            def validate_birth_date(self, birth_date):
                if birth_date > datetime.date.today():
                    raise ValidationError('Data de nascimento não pode ser no futuro.')

        class BookSchema(ma.SQLAlchemyAutoSchema):
            class Meta:
                model = Book

            id = fields.Int(dump_only=True)
            title = fields.Str(required=True, min_length=3, max_length=100, error_messages={'required': 'O título é obrigatório', 'min_length': 'O título deve ter no mínimo 3 caracteres'})
            publication_date = fields.Date(required=True, error_messages={'required': 'A data de publicação é obrigatória', 'type': 'Data de publicação inválida'})
            number_pages = fields.Int(required=True, min_value=1, error_messages={'required': 'O número de páginas é obrigatório', 'type': 'Número de páginas inválido', 'min_value': 'O número de páginas deve ser maior que 0'})
            authors_id = fields.Int(required=True, error_messages={'required': 'O ID do autor é obrigatório'})
            authors_name = fields.Str(dump_only=True)

        author_schema = AuthorsSchema()
        authors_schema = AuthorsSchema(many=True)
        book_schema = BookSchema()
        books_schema = BookSchema(many=True)

        @app.errorhandler(ValidationError)
        def handle_validation_error(e):
            return jsonify(e.messages), 400

        @app.errorhandler(404)
        def resource_not_found(e):
            return jsonify({'message': 'Recurso não encontrado'}), 404

        @app.errorhandler(Exception)
        def handle_exception(e):
            app.logger.error(f'Unhandled Exception: {str(e)}')
            return jsonify({'message': 'Ocorreu um erro interno no servidor'}), 500

        @app.route('/')
        def index():
            return jsonify({'message': 'API is running'}), 200

        # CRUD AUTORES

        @api.route('/authors')
        class AuthorsResource(Resource):
            @api.doc(description='Get all authors')
            def get(self):
                authors = Author.query.all()
                return authors_schema.dump(authors), 200 if authors else 404

            @api.doc(description='Create a new author')
            @api.expect(author_schema)
            def post(self):
                try:
                    data = request.get_json()
                    author = author_schema.load(data)
                    new_author = Author(**author)
                    db.session.add(new_author)
                    db.session.commit()
                    return author_schema.dump(new_author), 201
                except ValidationError as err:
                    return err.messages, 400
                except Exception as e:
                    app.logger.error(f'Error creating author: {str(e)}')
                    return {'message': 'Erro ao criar autor'}, 500

        @api.route('/authors/<int:id>')
        class AuthorResource(Resource):
            @api.doc(description='Get an author by ID')
            def get(self, id):
                author = Author.query.get(id)
                if not author:
                    return {'message': 'Autor não encontrado'}, 404
                return author_schema.dump(author), 200

            @api.doc(description='Update an author by ID')
            @api.expect(author_schema)
            def put(self, id):
                try:
                    data = request.get_json()
                    author = Author.query.get(id)
                    if not author:
                        return {'message': 'Autor não encontrado'}, 404

                    updated_fields = author_schema.load(data, partial=True)
                    for key, value in updated_fields.items():
                        setattr(author, key, value)

                    db.session.commit()
                    return author_schema.dump(author), 200
                except ValidationError as err:
                    return err.messages, 400
                except Exception as e:
                    app.logger.error(f'Error updating author: {str(e)}')
                    return {'message': 'Erro ao atualizar autor'}, 500

            @api.doc(description='Delete an author by ID')
            def delete(self, id):
                try:
                    author = Author.query.get(id)
                    if not author:
                        return {'message': 'Autor não encontrado'}, 404

                    db.session.delete(author)
                    db.session.commit()
                    return {'message': 'Autor removido com sucesso!'}, 200
                except Exception as e:
                    app.logger.error(f'Error deleting author: {str(e)}')
                    return {'message': 'Erro ao remover autor'}, 500

        # CRUD LIVROS

        @api.route('/books')
        class BooksResource(Resource):
            @api.doc(description='Get all books')
            def get(self):
                books = Book.query.all()
                return books_schema.dump(books), 200 if books else 404

            @api.doc(description='Create a new book')
            @api.expect(book_schema)
            def post(self):
                try:
                    data = request.get_json()
                    book = book_schema.load(data)
                    if book['number_pages'] == 0:
                        return {'message': 'O livro não pode ter zero páginas'}, 400

                    author = Author.query.get(book['authors_id'])
                    if not author:
                        return {'message': 'Autor não cadastrado'}, 400

                    new_book = Book(**book)
                    db.session.add(new_book)
                    db.session.commit()
                    return book_schema.dump(new_book), 201
                except ValidationError as err:
                    return err.messages, 400
                except Exception as e:
                    app.logger.error(f'Error creating book: {str(e)}')
                    return {'message': 'Erro ao criar livro'}, 500

        @api.route('/books/<int:id>')
        class BookResource(Resource):
            @api.doc(description='Get a book by ID')
            def get(self, id):
                book = Book.query.get(id)
                if not book:
                    return {'message': 'Livro não encontrado'}, 404
                return book_schema.dump(book), 200

            @api.doc(description='Update a book by ID')
            @api.expect(book_schema)
            def put(self, id):
                try:
                    data = request.get_json()
                    book = Book.query.get(id)
                    if not book:
                        return {'message': 'Livro não encontrado'}, 404

                    updated_fields = book_schema.load(data, partial=True)
                    for key, value in updated_fields.items():
                        setattr(book, key, value)

                    db.session.commit()
                    return book_schema.dump(book), 200
                except ValidationError as err:
                    return err.messages, 400
                except Exception as e:
                    app.logger.error(f'Error updating book: {str(e)}')
                    return {'message': 'Erro ao atualizar livro'}, 500

            @api.doc(description='Delete a book by ID')
            def delete(self, id):
                try:
                    book = Book.query.get(id)
                    if not book:
                        return {'message': 'Livro não encontrado'}, 404

                    db.session.delete(book)
                    db.session.commit()
                    return {'message': 'Livro removido com sucesso!'}, 200
                except Exception as e:
                    app.logger.error(f'Error deleting book: {str(e)}')
                    return {'message': 'Erro ao remover livro'}, 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)