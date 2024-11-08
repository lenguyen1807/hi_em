# from hi_em.scanner.scanner import Scanner
import click
from hi_em.hi_em import HiEm


@click.command()
@click.option("--path", default=None)
def main(path):
    if path:
        HiEm.run_file(path)
    else:
        HiEm.run_prompt()


if __name__ == "__main__":
    # main()
    HiEm.run_file("./example/test.hiem")
