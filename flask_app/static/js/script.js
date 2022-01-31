function getBackgroundColor(num){ // use dictionary to clean up later
    // var colorDict = {
    // };
    if (num>=1 && num<2){
        return("#9A70A0");
    }
    if (num>=2 && num<3){
        return("#b36fac");
    }
    if (num>=3 && num<4){
        return("#c46e97");
    }
    if (num>=4 && num<5){
        return("#e06e6e");
    }
    if (num>=5 && num<6){
        return("#d9764c");
    }
    if(num>=6 && num<7){
        return("#e88d4d");
    }
    if (num>=7 && num<8){
        return("#f2ba35");
    }
    if (num>=8 && num<9){
        return("#b5a04c");
    }
    if (num>=9 && num<10){
        return("#85945d");
    }
    if(num==10){
        return("#657B62");
    }
}

// function setBackgroundColor(){
//     // $(this).css(backgroundColor:"green");
//     console.log( document.querySelector("home-number-block"));
//     document.querySelector("home-number-block").style.backgroundColor = "green";
// }

// function backgroundColorGet
// reports page update display to be slidebar number
function updateLabel() {  
    // update individual sliders
    let range_val = this.parentElement.getElementsByClassName("range-value")[0];
    let current_val = parseFloat(range_val.innerHTML);
    let new_val = parseFloat(this.value);
    range_val.innerHTML = new_val; // update the individual slider with slider val
    range_val.style.backgroundColor = getBackgroundColor(new_val);

    // now update the overall number
    let avg_val = parseFloat(document.querySelector("#daily-number").innerHTML);
    let avg_val_rounded = avg_val;
    if (current_val != new_val){
        let add_by =(new_val-current_val)/num_sliders;
        avg_val = avg_val + add_by;
        avg_val_rounded = Math.round((avg_val)*100)/100; 
    }
    document.querySelector("#daily-number-view").style.backgroundColor = getBackgroundColor(avg_val_rounded);
    // console.log(document.querySelector("#daily-number").style);
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

// Color Mapping




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

//automatically set colors for home