import click

@click.group()
@click.version_option(version="1.0.0")
def cli():
    pass

@cli.command()
def examples():
    examples_data = [
        {
            "name": "Exemplo 1: Compra e venda com lucro",
            "explanation": "Compra 10k ações a R$ 10,00, vende 5k a R$ 20,00. Lucro de R$ 50k, imposto de 20% = R$ 10k"
        },
    ]
    
    for example in examples_data:
        click.echo(f"{'='*60}")
        click.echo(f"{example['name']}")
        click.echo(f"Example: {example['explanation']}")
        click.echo(f"{'='*60}")
        click.echo(f"\n")


if __name__ == "__main__":
    cli()