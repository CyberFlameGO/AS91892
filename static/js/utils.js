function changeImage () { // eslint-disable-line no-unused-vars
    
  if (document.getElementById("swapImg").src === 'https://www.paghat.com/empireofthechihuahua/chi-by-raptorwitness.jpg') {
      document.getElementById("swapImg").src = 'https://i.huffpost.com/gen/1619949/thumbs/o-121255937-570.jpg?1'
  } else {
      document.getElementById("swapImg").src = 'https://www.paghat.com/empireofthechihuahua/chi-by-raptorwitness.jpg'
  }
}

const clickCount = document.getElementById('clicks');

let clicks = 0;

function incrementClickCount () { // eslint-disable-line no-unused-vars
  clicks++;
  clickCount.innerHTML = clicks;
}
