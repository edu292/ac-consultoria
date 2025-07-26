import sqlite3
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from main.models import Ocorrencia


class Command(BaseCommand):
    help = 'Imports location data from a standalone SQLite database into the LocationEvent table.'

    def add_arguments(self, parser):
        parser.add_argument('sqlite_file', type=str, help='The path to the SQLite database file.')

    def handle(self, *args, **options):
        sqlite_file_path = options['sqlite_file']

        self.stdout.write(self.style.NOTICE(f"Connecting to SQLite DB at {sqlite_file_path}..."))

        try:
            conn = sqlite3.connect(sqlite_file_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM alvos")
            rows = cursor.fetchall()

            locations_to_create = []
            for row in rows:
                datetime_string = str(row['data'])

                date_object = datetime.fromisoformat(datetime_string).date()
                locations_to_create.append(
                    Ocorrencia(
                        nome=row['nome'],
                        numero_documento=row['id'],
                        numero_bo=row['bo'],
                        cidade=row['cidade'],
                        placa=row['placa'],
                        delito=row['delito'],
                        data=date_object,
                        estrutura_criminal=row['estrutura criminal']
                    )
                )

            if locations_to_create:
                Ocorrencia.objects.bulk_create(locations_to_create)
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(locations_to_create)} locations.'))
            else:
                self.stdout.write(self.style.WARNING('No locations found to import.'))

        except FileNotFoundError:
            raise CommandError(f'Error: The file at "{sqlite_file_path}" was not found.')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')
        finally:
            if 'conn' in locals() and conn:
                conn.close()