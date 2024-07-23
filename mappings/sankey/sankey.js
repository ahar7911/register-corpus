google.charts.load('current', {'packages':['sankey']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
    var CONVERSION = 218/45;
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'From');
    data.addColumn('string', 'To');
    data.addColumn('number', 'Weight');
    data.addRows([
        [ 'CORE: Informational Description/Explanation', 'Informational Description/Explanation', 10*CONVERSION ],
        [ 'CORE: Narrative', 'Recreational Narrative', 1*CONVERSION ],
        [ 'CORE: Narrative', 'Journalistic Narrative', 6*CONVERSION ],
        [ 'CORE: Narrative', 'Unused', 1*CONVERSION ],
        [ 'CORE: Informational Persuasion', 'Informational Persuasion/Opinion', 4*CONVERSION ],
        [ 'CORE: Opinion', 'Informational Persuasion/Opinion', 4*CONVERSION ],
        [ 'CORE: How-to/Instructional', 'How-to/Instructional', 5*CONVERSION ],
        [ 'CORE: Lyrical', 'Lyrical', 4*CONVERSION ],
        [ 'CORE: Interactive Discussion', 'Natural Interactive Discussion', 4*CONVERSION ],
        [ 'CORE: Spoken', 'Natural Interactive Discussion', 1*CONVERSION ],
        [ 'CORE: Spoken', 'Unused', 3*CONVERSION ],
        [ 'CORE: Spoken', 'Artificial Interactive Discussion', 1*CONVERSION ],
        [ 'Informational Description/Explanation', 'CAHIER: actes juridiques', 13 ],
        [ 'Unused', 'CAHIER: autres genres', 3 ],
        [ 'Informational Persuasion/Opinion', 'CAHIER: genres argumentatifs', 7 ],
        [ 'Natural Interactive Discussion', 'CAHIER: genres argumentatifs', 1 ],
        [ 'Lyrical', 'CAHIER: genres argumentatifs', 1 ],
        [ 'Informational Description/Explanation', 'CAHIER: genres argumentatifs', 1 ],
        [ 'Informational Description/Explanation', 'CAHIER: genres descriptifs et expositifs', 22 ],
        [ 'Journalistic Narrative', 'CAHIER: genres descriptifs et expositifs', 1 ],
        [ 'Informational Persuasion/Opinion', 'CAHIER: genres descriptifs et expositifs', 2 ],
        [ 'How-to/Instructional', 'CAHIER: genres descriptifs et expositifs', 3 ],
        [ 'Natural Interactive Discussion', 'CAHIER: genres epistolaires/correspondances', 5 ],
        [ 'Journalistic Narrative', 'CAHIER: genres journalistiques', 5 ],
        [ 'Informational Description/Explanation', 'CAHIER: genres lexicographiques', 14 ],
        [ 'Recreational Narrative', 'CAHIER: genres narratifs', 40 ],
        [ 'Informational Description/Explanation', 'CAHIER: genres narratifs', 3 ],
        [ 'Journalistic Narrative', 'CAHIER: genres narratifs', 2 ],
        [ 'Lyrical', 'CAHIER: genres narratifs', 2 ],
        [ 'Unused', 'CAHIER: genres narratifs', 1 ],
        [ 'Artificial Interactive Discussion', 'CAHIER: genres narratifs', 1 ],
        [ 'Lyrical', 'CAHIER: genres poetiques', 39 ],
        [ 'Recreational Narrative', 'CAHIER: genres poetiques', 1 ],
        [ 'Artificial Interactive Discussion', 'CAHIER: genres theatraux', 30 ],
        [ 'Informational Description/Explanation', 'CAHIER: paratextes', 9 ],
        [ 'Unused', 'CAHIER: genres gnomiques', 8 ],
        [ 'Informational Description/Explanation', 'CAHIER: genres gnomiques', 2 ],
        [ 'Recreational Narrative', 'CAHIER: genres gnomiques', 2 ],
  ]);

  // Sets chart options.
  var options = {
    width: 1000,
  };

  // Instantiates and draws our chart, passing in some options.
  var chart = new google.visualization.Sankey(document.getElementById('sankey_basic'));
  chart.draw(data, options);
}