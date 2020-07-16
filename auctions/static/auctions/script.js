document.addEventListener('DOMContentLoaded', function() {
    var elem = document.querySelector('.sidenav');
    var instance = M.Sidenav.init(elem);
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
    var elem = document.querySelector('.materialboxed');
    var instance = M.Materialbox.init(elem);
  });