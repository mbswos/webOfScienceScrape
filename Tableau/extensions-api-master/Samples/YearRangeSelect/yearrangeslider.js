'use strict';

(function () {
  $(document).ready(function () {
    // This is the entry point into the extension.  It initializes the Tableau Extensions Api, and then
    // grabs all of the parameters in the workbook, processing each one individually.
    tableau.extensions.initializeAsync().then(function () {
      tableau.extensions.dashboardContent.dashboard.getParametersAsync().then(function (parameters) {
        parameters.forEach(function (p) {
          //p.addEventListener(tableau.TableauEventType.ParameterChanged, onParameterChange);
        });
      });
    });

    setDateRangeFilter(1970, 2019);
  });

  // When the parameter is changed, we recreate the row with the updated values.  This keeps the code
  // clean, and emulates the approach that something like React does where it "rerenders" the UI with
  // the updated data.
  //
  // To avoid multiple layout processing in the browser, we build the new row unattached to the DOM,
  // and then attach it at the very end.  This helps avoid jank.
  function onParameterChange (parameterChangeEvent) {
    parameterChangeEvent.getParameterAsync('Start Year').then(function (param) {
      var start_year = param.currentValue.formattedValue;
      var end_year = $('#year-range-slider').getValue()[1];
      updateSliderValues(start_year, end_year)
    });

    parameterChangeEvent.getParameterAsync('End Year').then(function (param) {
      var start_year = $('#year-range-slider').getValue()[0];
      var end_year = param.currentValue.formattedValue;
      updateSliderValues(start_year, end_year)
    });
  }

  function updateSliderValues(start_year, end_year){
    var new_value = [start_year, end_year];
    $('#year-range-slider').setValue(new_value,false,false);
  }

  function updateParameter(param_name, value){
    tableau.extensions.dashboardContent.dashboard.getParametersAsync().then(function (parameters){
      parameters.forEach(function (param) {
        if(param.name === param_name){
          param.changeValueAsync(value);
        }
        console.log(1)
      });
    });
  }

  function setDateRangeFilter(min, max){
    var years = [];
    var year_ticks = [];
    for (var i = min; i < max + 5; i+=5){
        year_ticks.push(i);
    }

    var UpdateParams = function(event){
      var start_year = event.value[0];
      var end_year = event.value[1];
      updateParameter('Start Year', start_year)
      updateParameter('End Year', end_year)
    }

    var slider = $("#year-range-slider").slider({    
      id: 'year-range-slider',
      step:1,
      value:[min, max],
      ticks:year_ticks,
      ticks_labels:year_ticks,
      tooltip_split: true,
      tooltip: 'always'
    }).on('slideStop', UpdateParams);

    return slider;
  }
})();
