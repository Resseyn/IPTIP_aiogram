let counts = [1, 1]

function updateButtons() {
    document.querySelectorAll(".incButton").forEach((button, index) => {
        let newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);

        newButton.addEventListener("click", function(){
            counts[index]++;
            document.querySelectorAll(".tab")[index].textContent = "Количество покупок:" + counts[index]
        })
    })

    document.querySelectorAll(".del").forEach((button, index) => {
        let newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);

        newButton.addEventListener("click", function(){
            document.querySelectorAll(".card")[index].remove()
            counts.splice(index, 1)
            updateButtons()
        })
    })
}

updateButtons()
