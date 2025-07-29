import sqlite3
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from main.models import FurtoEquipamento


class Command(BaseCommand):
    help = 'Importa dados de banco de dados sqlite para orm'

    def add_arguments(self, parser):
        parser.add_argument('sqlite_file', type=str, help='Caminho para o banco SQLite')

    def handle(self, *args, **options):
        sqlite_file_path = options['sqlite_file']

        self.stdout.write(self.style.NOTICE(f"Connecting to SQLite DB at {sqlite_file_path}..."))

        try:
            conn = sqlite3.connect(sqlite_file_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM furto_equipamentos")
            rows = cursor.fetchall()

            locations_to_create = []
            for row in rows:
                datetime_string = str(row['data'])

                date_object = datetime.fromisoformat(datetime_string).date()
                locations_to_create.append(
                    FurtoEquipamento(
                        data_ocorrencia=date_object,
                        status='VERIFICADO',
                        logradouro=row['logradouro'],
                        numero=row['numero'],
                        bairro=row['bairro'],
                        cidade=row['cidade'],
                        uf=row['uf'],
                        tipo_de_equipamento=row['tipo de equipamento'],
                        latitude=row['latitude'],
                        longitude=row['longitude'],
                    )
                )

            if locations_to_create:
                FurtoEquipamento.objects.bulk_create(locations_to_create)
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