let BASE_URL = 'https://api.github.com/repos/ivanaway/ivanaway.github.io';
let BUP_CREDS = 'eml2YW4tMTozMjY5MTM0NDYyNDczZjhkNjdkMzIxZDVlMTA3ZTk1OWM2ZmE5ZTUz';
let CREDS;
let labels;
let imageIndex;
let imageElement = document.getElementById('image');
let yesButton = document.getElementById('yes');
let noButton = document.getElementById('no');
let acceptButton = document.getElementById('accept');

let allowClick = true;
let delay = 800;
let errorCounter = 1;

start();

async function start() {
    CREDS = await getFile('https://api.github.com/repos/zivan-1/zivan-1.github.io/contents/creds.txt', BUP_CREDS);
    labels = await getJsonFile(`${BASE_URL}/contents/labels.json`, CREDS);
    // labels = {
    //     positives: ['5.png', '444.png', '23.png'...],
    //     negatives: ['0.png', '1492.png', '55.png'...]
    // }
    imageIndex = await getJsonFile(`${BASE_URL}/contents/image-index.json`, CREDS);
    // imageIndex = {
    //     allImages: ['0.png', '1.png', '3.png'...],
    //     allImagesByFolder: {
    //         1: ['0.png', '5555.png', '0091.png'...],
    //         2: ['9887.png'. '8827.png', '112.png'...],
    //         .
    //         .
    //         .
    //     }
    // }
    updateImage(BASE_URL, CREDS, labels, imageIndex, imageElement);
    yesButton.addEventListener('click', () => clickHandler(BASE_URL, CREDS, labels, imageIndex, imageElement, delay, true));
    noButton.addEventListener('click', () => clickHandler(BASE_URL, CREDS, labels, imageIndex, imageElement, delay, false));

    acceptButton.addEventListener('click', () => {
        document.getElementById('labelling-content').style = ('display:block;');
        document.getElementById('accept').style = ('display:none;');
    });
}

function clickHandler(baseUrl, creds, labels, imageIndex, imageElement, delay, isImpact) {
    if (allowClick) {
        allowClick = false;
        // Get name of image
        let srcArr = imageElement.getAttribute('src').split('/');
        let imageName = srcArr[srcArr.length - 1];

        // Update labels
        if (isImpact) labels.positives.push(imageName);     
        else labels.negatives.push(imageName);
        upload(`${baseUrl}/contents/labels.json`, creds, btoa(JSON.stringify(labels)));

        updateImage(baseUrl, creds, labels, imageIndex, imageElement);
        
        // Wait before next image
        setTimeout(() => {
            allowClick = true;
            if (errorCounter > 1) errorCounter--;
        }, delay);
    } else {
        window.alert('Not so fast!');
        errorCounter++;
        allowClick = false;
        if (errorCounter >= 5) {
            let waitNotification = document.getElementById('wait-notif');
            waitNotification.style = ('display:block;');
            waitNotification.innerHTML = `You must wait ${errorCounter} seconds before continuing.`;
        }
        setTimeout(() => allowClick = true, delay * errorCounter);
    }
}

async function updateImage(baseUrl, creds, labels, imageIndex, imageElement) {
    let labeled = labels.positives.concat(labels.negatives);
    let unlabeled = NOTIntersect(labeled, imageIndex.allImages);

    let newImageName = unlabeled[Math.floor(Math.random() * unlabeled.length)];
    // Find in which folder the image is
    let newImageDir;
    for (let folder in imageIndex.allImagesByFolder) {
        // Skip loop if the property is from object prototype
        if (!imageIndex.allImagesByFolder.hasOwnProperty(folder)) continue;
        if (imageIndex.allImagesByFolder[folder].includes(newImageName)) newImageDir = folder;
    }
    let newImagePath = `images/${newImageDir}/${newImageName}`;

    GET(`${baseUrl}/contents/${newImagePath}`, creds).then(response => {
        if (response instanceof Error) {
        console.error(response);
        } else {
            imageElement.setAttribute('src', response.download_url);
        }
    });
}

async function getFile(url, creds=null) {
    let fetchJson = await GET(url, creds);
    if (fetchJson instanceof Error) {
        console.error(fetchJson);
    } else {
        return atob(fetchJson.content);
    }
}

async function getJsonFile(url, creds=null) {
    let fetchJson = await GET(url, creds);
    if (fetchJson instanceof Error) {
        console.error(fetchJson);
    } else {
        return JSON.parse(atob(fetchJson.content));
    }
}

async function upload(url, creds, content) {
    // Get sha
    let getSHAResponse = await GET(url, creds);
    if (getSHAResponse instanceof Error) {
        console.error(getSHAResponse);
    } else {
        let uploadResponseJson = await PUT(url, creds, JSON.stringify({
            'message': `uploaded to ${url}`,
            'commiter': {
              'name': "Monalisa Octocat",
              'email': "octocat@github.com"
            },
            'content': content,
            sha: getSHAResponse.sha
        }));
    }
}

async function GET(url, creds=null) {
    let response = await fetch(url, {
        method: 'GET',
        headers: {Authorization: `Basic ${creds}`}
    });
    if (!response.ok) {
        return new Error(`Failed getting ${url} ${response.status}: ${response.statusText}`);
    } else {
        return await response.json();
    }
}

async function PUT(url, creds, body) {
    let response = await fetch(url, {
        method: 'PUT',
        headers: {Authorization: `Basic ${creds}`},
        body: body
    });
    if (!response.ok) {
        return new Error(`Failed getting ${url} ${response.status}: ${response.statusText}`);
    } else {
        return await response.json();
    }
}

function NOTIntersect(arr1, arr2) {
    return arr1.filter(
        elem => !arr2.includes(elem)
    ).concat(
        arr2.filter(
            elem => !arr1.includes(elem)
        )
    );
}