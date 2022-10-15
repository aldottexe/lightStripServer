def gradient (LED_COUNT: int, rgb1 = [255,0,0], rgb2 = [128,0,255], offset=0):
    offset = min(offset, LED_COUNT - 1)
    result = []
    rgbCopy = list(rgb1)
   
    increments = [(c2 - c1) / (LED_COUNT - 1) for c1, c2 in zip(rgb1, rgb2)]

    print("LINE HERE")
    print("increments", increments)
    print("LINE HERE")

    for i in range(LED_COUNT-offset):
        result.append([round(rgb1[0]), round(rgb1[1]), round(rgb1[2])])
        rgb1 = [val + increment for val, increment in zip(rgb1, increments)]
        print(i, rgb1)

    for _ in range(offset):
        rgbCopy = [color + increment for color, increment in zip(rgbCopy, increments)]
        result[:0] = [[round(rgbCopy[0]), round(rgbCopy[1]), round(rgbCopy[2])]]

    return result
if __name__ == "__main__":
    print(gradient(5,[1,1,1],[5,5,5],3))