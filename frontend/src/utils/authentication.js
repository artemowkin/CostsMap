export const checkAuthentication = () => {
    try {
        const token = JSON.parse( localStorage.getItem('tokenData') )
        const nowDate = new Date()
        const nowTimeStamp = nowDate.getTime() / 1000

        if (!token) throw 'NoToken'

        if (nowTimeStamp >= token.exptime) throw 'TokenExpired'

        return true
    } catch {
        return false
    }
}