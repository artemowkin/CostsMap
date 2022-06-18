export const roundDecimal = (decimal) => {
    if (isNaN(decimal))
        return 0

    return Math.trunc(decimal * 100) / 100
}