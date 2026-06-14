import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from subunidade.models import Subunidade

DEFAULT_CSV = r"C:\Users\loren\OneDrive\Desktop\unidades_ufsm.csv"

TIPOS_RELEVANTES = {
    "Departamento Didático",
    "Subunidade Acadêmica",
    "Subunidade Administrativa",
    "Coordenação Acadêmica",
}

SITUACOES_ATIVAS = {"Formal", "Interna", "Informal", "Nova"}


class Command(BaseCommand):
    help = "Importa as unidades da UFSM do CSV (upsert por COD_ESTRUTURADO)."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", nargs="?", default=DEFAULT_CSV)

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"])
        if not csv_path.exists():
            self.stderr.write(self.style.ERROR(f"CSV nao encontrado: {csv_path}"))
            return

        criados = atualizados = ignorados = 0

        # O CSV é UTF-8 (utf-8-sig tolera BOM se houver).
        with csv_path.open(encoding="utf-8-sig") as handle:
            reader = csv.DictReader(line for line in handle if line.strip())
            for row in reader:
                tipo = (row.get("TIPO_UNIDADE") or "").strip()
                situacao = (row.get("SITUACAO") or "").strip()
                cod = (row.get("COD_ESTRUTURADO") or "").strip()

                if tipo not in TIPOS_RELEVANTES or situacao not in SITUACOES_ATIVAS or not cod:
                    ignorados += 1
                    continue

                _, created = Subunidade.objects.update_or_create(
                    cod_estruturado=cod,
                    defaults={
                        "nome": (row.get("NOME_UNIDADE") or "").strip(),
                        "centro_nome": (row.get("NOME_CENTRO") or "").strip(),
                        "centro_sigla": (row.get("SIGLA_CENTRO") or "").strip(),
                        "tipo": tipo,
                        "situacao": situacao,
                        "ativo": True,
                    },
                )
                if created:
                    criados += 1
                else:
                    atualizados += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Importacao concluida: {criados} criados, {atualizados} atualizados, "
                f"{ignorados} ignorados. Total na base: {Subunidade.objects.count()}."
            )
        )
