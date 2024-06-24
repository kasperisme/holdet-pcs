from src import pcs_formater, holdet_formater, datagather, optimize


def main():
    holdet_formater.main()
    pcs_formater.main()
    datagather.main()
    optimize.main()

    return 200


if __name__ == "__main__":
    main()
