let selection = 1;

function changeSelection(event) {
    selection = event.target.value
}

function displayCsvData(data) {
    let csvDataDiv = document.getElementById('csv-data');
    let tempDiv = document.createElement('div');
    tempDiv.innerHTML = data;
    let csvTable = tempDiv.querySelector('table');
    let buttonCell = document.createElement('td');
    buttonCell.textContent = 'Click to Predict';
    csvTable.rows[0].appendChild(buttonCell);
    // Create a new row at the end of the table with a button element
    for (let i = 1; i < csvTable.rows.length; i++) {
        // Create a new cell in the row with a button element
        let buttonCell = document.createElement('td');
        let button = document.createElement('button');
        button.textContent = 'Predict';
        buttonCell.appendChild(button);
        csvTable.rows[i].appendChild(buttonCell);

        button.addEventListener('click', function () {

            let myButton = document.getElementById('my-button');
            let popup = document.getElementById('popup');
            let backdrop = document.getElementById('backdrop');
            popup.style.display = 'block';
            backdrop.style.display = 'block';

            let row = this.parentNode.parentNode;
            let storypointCell = row.querySelector('td:nth-child(4)');

            let descriptionCell = row.querySelector('td:nth-child(3)');
            let descriptionValue = descriptionCell.textContent;

            let request = new XMLHttpRequest();
            request.open('POST', 'http://127.0.0.1:5000/userStory?choice=' + selection, true);
            request.setRequestHeader('Content-Type', 'application/json');
            request.onload = function () {
                if (request.status >= 200 && request.status < 400) {
                    // Success!
                    let data = request.responseText;
                    let val = JSON.parse(data);
                    let storyPoint = val.story_point;
                    storypointCell.textContent = storyPoint;
                    console.log(storyPoint);
                } else {
                    // We reached our target server, but it returned an error
                }
                document.getElementById('loading-indicator').style.display = 'none';
                popup.style.display = 'none';
                backdrop.style.display = 'none';
            };
            request.onerror = function () {
                document.getElementById('loading-indicator').style.display = 'none';
                popup.style.display = 'none';
                backdrop.style.display = 'none';
                // There was a connection error of some sort
            };
            let userStory = {
                user_story: descriptionValue
            };
            document.getElementById('loading-indicator').style.display = 'block';
            let data = JSON.stringify(userStory);
            request.send(data);


        });
    }
    console.log(csvTable)
    // Append the table to the 'csv-data' div element
    csvDataDiv.appendChild(csvTable);

    let csvButton = document.createElement('button');
    csvButton.textContent = 'Download CSV';
    csvDataDiv.appendChild(csvButton);
    csvButton.addEventListener('click', function () {
        // Convert the HTML table to a CSV string
        let csvData = csvTableToCsv(csvTable);

        // Create a new blob object with the CSV data
        let blob = new Blob([csvData], {type: 'text/csv;charset=utf-8;'});

        // Create a new URL for the blob object
        let url = URL.createObjectURL(blob);

        // Create a new anchor element with the URL as the href attribute
        let downloadLink = document.createElement('a');
        downloadLink.href = url;
        downloadLink.download = 'data.csv';

        // Append the anchor element to the document body and click it to start the download
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
    });
}

function csvTableToCsv(table) {
    let csvRows = [];

    for (let i = 0; i < table.rows.length; i++) {
        let csvCells = [];
        for (let j = 0; j < table.rows[i].cells.length; j++) {
            csvCells.push(table.rows[i].cells[j].textContent);
        }
        csvRows.push(csvCells.join(','));
    }

    return csvRows.join('\n');
}

function handleFileSelect(event) {
    let file = event.target.files[0];
    let formData = new FormData();
    formData.append('file', file);
    console.log(file)
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/multiple_prediction');
    xhr.onload = function () {
        if (xhr.status === 200) {
            displayCsvData(xhr.responseText);
        } else {
            alert('Error uploading file');
        }
    };
    xhr.send(formData);
}
