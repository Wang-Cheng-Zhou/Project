"""求解“公鸡5元一只，母鸡3元一只，小鸡1元三只，100块钱买100只鸡”的组合。"""

if __name__ == "__main__":
    solutions = []

    for roosters in range(21):
        for hens in range(34):
            chicks = 100 - roosters - hens
            if chicks < 0:
                break
            if chicks % 3 != 0:
                continue
            total_cost = 5 * roosters + 3 * hens + chicks // 3
            if total_cost == 100:
                solutions.append((roosters, hens, chicks))

    if not solutions:
        print("没有符合条件的组合。")
    else:
        print("符合条件的鸡只组合：")
        for roosters, hens, chicks in solutions:
            print(f"公鸡：{roosters} 只，母鸡：{hens} 只，小鸡：{chicks} 只")
