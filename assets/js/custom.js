function addEditButtons(el) {
    $(el).append('<div class="fa-solid fa-pen-to-square btn-light"></div>')
    $(el).append('<div class="fa-solid fa-up-down-left-right btn-light"></div>')
    $(el).append('<div class="fa-solid fa-trash btn-light"></div>')

    $(el).find('.fa-pen-to-square').on('click', function() {
    setTimeout(function () {$('#syncStore').click()},100)
    setTimeout(function() {$("#editActive").click()}, 300)})

    $(el).find('.fa-trash').on('click', function() {
        setTimeout($('#syncStore').click(),100)
        setTimeout( function () {
        if (confirm('Are you sure you want to delete, you cannot recover')) {
        $("#deleteTarget").click()}}, 300)
    })
}


function dragElement(elmnt) {

  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  $(elmnt).on('mousedown', function(e) {
    dragMouseDown(e)
  })

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // posición del mouse al inicio:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calcular la posición del cursor:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // cambiar la posición del elemento:
    $(elmnt).closest('.dash-graph')[0].style.top = ($(elmnt).closest('.dash-graph')[0].offsetTop - pos2) + "px";
    $(elmnt).closest('.dash-graph')[0].style.left = ($(elmnt).closest('.dash-graph')[0].offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    // Detener movimiento cuando se suelta el mouse:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}