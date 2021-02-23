from subprocess import run

def main():
    run(['powershell', '-Command', 'jupyter nbconvert C:/Users/omgda/Desktop/StockBot/NeuralNetwork.ipynb --to="python" --output-dir="C:/Users/omgda/Desktop/StockBot/"'])