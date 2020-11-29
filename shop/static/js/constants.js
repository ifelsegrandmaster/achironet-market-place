const ACHIRONET_HOSTNAME = '192.168.43.159:8000'
const ACHIRONET_PROTOCOL = 'http'

// check if this device is mobile
function detectMob() {
    const toMatch = [
        /Android/i,
        /webOS/i,
        /iPhone/i,
        /iPad/i,
        /iPod/i,
        /BlackBerry/i,
        /Windows Phone/i
    ];

    return toMatch.some((toMatchItem) => {
        return navigator.userAgent.match(toMatchItem);
    });
}

window.mobileCheck = detectMob()