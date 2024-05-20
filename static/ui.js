"use strict";
document.addEventListener('DOMContentLoaded', function () {
    let num_fields = 0;
    let form = document.forms[0];
    let fg = form.querySelectorAll(".form-group");
    if (fg == null) {
        console.log(`fg == null: ${fg == null}`);
        return;
    }
    num_fields = fg.length;

    // fg[0].innerHTML = fg[0].innerHTML.replaceAll('Точка 0', 'Начало');
    let but_grp = document.querySelector("#queryAction");
    if (but_grp == null) {
        console.log(`but_grp == null: ${but_grp == null}`);
        return;
    }
    let sbut = but_grp.querySelector("button[type='button']");
    if (sbut == null) {
        console.log(`sbut == null: ${sbut == null}`);
        return;
    }
    sbut.addEventListener('click', () => {
        var doc = document.createElement('div');
        doc.innerHTML =
            '<input type="text" name="FIELDNAME" value="" class="textinput form-control" required="" aria-describedby="id_FIELDNAME_helptext" id="id_FIELDNAME">' +
                '<small id="hint_id_FIELDNAME" class="form-text text-muted">Точка FIELDNAME</small>';
        doc.innerHTML = doc.innerHTML.replaceAll('FIELDNAME', `${num_fields}`);
        num_fields++;
        form.replaceChild(doc, but_grp);
        form.appendChild(but_grp);
    });
});
