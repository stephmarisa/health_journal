// reports page update display to be slidebar number and right color
function updateLabel() {  
    // update individual sliders
    let range_val = this.parentElement.getElementsByClassName("range-value")[0];
    let current_val = parseFloat(range_val.innerHTML);
    let new_val = parseFloat(this.value);
    range_val.innerHTML = new_val; // update the individual slider with slider val

    // now update the overall number
    let avg_val = parseFloat(document.querySelector("#daily-number").innerHTML);
    let avg_val_rounded = avg_val;
    if (current_val != new_val){
        let add_by =(new_val-current_val)/num_sliders;
        avg_val = avg_val + add_by;
        avg_val_rounded = Math.round((avg_val)*100)/100; 
    }
    console.log("val", current_val)
    document.querySelector("#daily-number").innerHTML = avg_val;
    document.querySelector("#daily-number-view").innerHTML = avg_val_rounded;
}
var slideContainers = document.getElementsByClassName("slidecontainer");
const num_sliders = slideContainers.length;

// update individual and overall value for every slide container
for (var i = 0; i < slideContainers.length; i++) {
    var slider = slideContainers[i].getElementsByClassName("slider")[0];
    updateLabel.call(slider);
    slider.oninput = updateLabel;
    // slider.oninput = updateAverage;
}



// Scrolling
let anchorSelector = 'a[href^="#"]';
let anchorList =
    document.querySelectorAll(anchorSelector);
anchorList.forEach(link => {
    link.onclick = function (e) {
        e.preventDefault();
        let destination =
            document.querySelector(this.hash);
        destination.scrollIntoView({
            behavior: 'smooth'
        });
    }
});