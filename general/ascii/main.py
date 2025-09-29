def main():
    chars = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]
    string = "".join([chr(c) for c in chars])
    print(string)
    


if __name__ == "__main__":
    main()
