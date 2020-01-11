
function buildCharts(tw_df) {

  // Use `d3.json` to fetch the twitter data for the plots
  // Build a Bubble Chart using the sample data
	
	d3.json(`analyze`).then(function(data) {
		var data = [{
			x: data.No_of_likes,
			y: data.Polarity,
			text: data.Handle,
			type: 'bubble',
			mode: 'markers',
			marker: {
			color: data.Sentiment,
			size: data.No_of_likes
			}
		}];
		
		var layout = {
			title: 'Twitter Analysis',
			xaxis: {
				title: {
				  text: 'No of Likes',
				}
			},
			yaxis: {
				title: {
				  text: 'Polarity',
				}
			}
			//showlegend: true,
		};
		
		Plotly.newPlot('bubble', data, layout);
	});

	d3.json(`analysis`).then(function(sample) {
		var sample = [
			{
			type: "indicator",
			mode: "gauge+number+delta",
			value: sample.Rating,
			title: { text: "IMDb Rating", font: { size: 24 } },
			text: ['0-1', 'ML4', 'ML3', 'ML2', 'ML1',  '6','7','8','9','10'],
			textinfo: 'text',
			textposition:'inside',
			//delta: { reference: 400, increasing: { color: "RebeccaPurple" } },
			gauge: {
			axis: { range: [null, 10], tickwidth: 1, tickcolor: "black" },
			bar: { color: "#061B2F" },
			bgcolor: "white",
			borderwidth: 2,
			bordercolor: "white",
			steps: [
				{ range: [0, 1], color: "#c5ba92" },
				{ range: [1, 2], color: "#ccbe8b" },
				{ range: [2, 3], color: "#d2c185" },
				{ range: [3, 4], color: "#d8c57f" },
				{ range: [4, 5], color: "#dfc978" },
				{ range: [5, 6], color: "#e5cc72" },
				{ range: [6, 7], color: "#ecd06b" },
				{ range: [7, 8], color: "#f2d465" },
				{ range: [8, 9], color: "#f9d75e" },
				{ range: [9, 10], color: "#ffdb58" }
			],
			threshold: {
			  line: { color: "red", width: 4 },
			  thickness: 0.75,
			  value: 490
			}
			  }
			}
		  ];
		  
		  var layout = {
			width: 500,
			height: 400,
			margin: { t: 25, r: 25, l: 25, b: 25 },
			//paper_bgcolor: "lavender",
			font: { color: "", family: "Arial" }
		  };
		  
		  Plotly.newPlot(gauge, sample, layout);
	});
	
}

function init() {
  // Grab a reference to the dropdown select element
//   var selector = d3.select("#selDataset");

//   // Use the list of sample names to populate the select options
//   d3.json("/names").then((sampleNames) => {
//     sampleNames.forEach((sample) => {
//       selector
//         .append("option")
//         .text(sample)
//         .property("value", sample);
//     });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    //buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  //buildMetadata(newSample);
}

// Initialize the dashboard
init();