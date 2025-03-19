from src import pcs_formater, holdet_formater, datagather, optimize, odds_formater


# Originale depreciation_factor var 0.5
# Efter første etape blev det ændret til 0.6
#


def main(starting_stage: int = 0, budget: int = 50000000):
    print("Foretager analyse for etapen:", starting_stage + 1)
    holdet_formater.main(round=starting_stage)
    odds_formater.main(round=starting_stage)
    pcs_formater.main()
    datagather.main()
    optimize.main(starting_stage=starting_stage, capacity=budget)

    return 200


if __name__ == "__main__":
    stage = 20
    budget = 61450394
    maxtransfer = budget * 0.01

    main(stage, budget - maxtransfer)
