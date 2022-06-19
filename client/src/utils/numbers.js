export const roundDecimal = (decimal) => {
    if (isNaN(decimal))
        return decimal

    return Math.round(decimal * 100) / 100
}