const ACHIRONET_HOSTNAME = 'achironetmarketplace.com'
const ACHIRONET_PROTOCOL = 'https'

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