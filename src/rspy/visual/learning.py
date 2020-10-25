import matplotlib.pyplot as plt

def plotHistory(history, figsize=(12, 4)):
    plt.figure(figsize=figsize)
    plt.style.use("ggplot")
    histKeys = history.history.keys()
    plotCnt = 0
    if 'loss' in histKeys: plotCnt += 1
    if 'accuracy' in histKeys: plotCnt += 1
    
    subPosition = 1
    if 'loss' in histKeys:
        plt.subplot(1, plotCnt, subPosition)
        plt.plot(history.history['loss'], 'b-', label='loss')
        if 'val_loss' in histKeys:
            plt.plot(history.history['val_loss'], 'r--', label='val_loss')
        plt.xlabel('Epoch')
        plt.legend()
        subPosition += 1

    if 'accuracy' in histKeys:
        plt.subplot(1, plotCnt, subPosition)
        plt.plot(history.history['accuracy'], 'g-', label='accuracy')
        if 'val_accuracy' in histKeys:
            plt.plot(history.history['val_accuracy'], 'k--', label='val_accuracy')
        plt.xlabel('Epoch')
        plt.ylim(0.7, 1)
        plt.legend()

    plt.show()
