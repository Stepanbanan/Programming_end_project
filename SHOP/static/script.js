function openNewListModal() {
    document.getElementById('modal').style.display = 'block';
}

function closeNewListModal() {
    document.getElementById('modal').style.display = 'none';
}

window.onclick = function(event) {
    if (event.target === document.getElementById('modal')) {
        closeNewListModal();
    }
}
