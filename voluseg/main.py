from dendro.sdk import App
from VolusegProcessor import VolusegProcessor


app = App(
    app_name='voluseg',
    description='Voluseg processors'
)

app.add_processor(VolusegProcessor)


if __name__ == '__main__':
    app.run()