var picker = null;
var opacity = 100;

var update = function () {
  data = {
    r: (picker.rgb[0]*255).toFixed(),
    g: (picker.rgb[1]*255).toFixed(),
    b: (picker.rgb[2]*255).toFixed(),
    a: parseInt($('#alpha').val(), 10)
  };

  $.post('api', data);
}

$.browser = {}

$(document).ready(function() {
  picker = $.farbtastic('#colorPicker', {});
  picker.setColor('#ffffff');

  $.getJSON('api', function(data) {
    color = picker.pack([data.r / 255, data.g / 255, data.b / 255]);
    picker.setColor(color);

    $('#alpha').val(data.a);

    $('#alpha').on('change', update);
    picker.linkTo(update);
  });
});
