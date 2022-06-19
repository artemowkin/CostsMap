export const roundDecimal = (decimal) => {
    if (isNaN(decimal))
        return 0

    return Math.round(decimal * 100) / 100
}