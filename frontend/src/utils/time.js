export const dateToLocalizedISO = (dateObj) => {
    const tzOffset = dateObj.getTimezoneOffset()
    const localizedDate = new Date(dateObj.getTime() - (tzOffset*60*1000))
    return localizedDate.toISOString().split('T')[0]
}