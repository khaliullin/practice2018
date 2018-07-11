let cy = cytoscape({
    container: document.getElementById('cy'),
    style: cytoscape.stylesheet()
        .selector('node')
        .css({
            'content': 'data(name)',
            'text-valign': 'center',
            'color': 'white',
            'text-outline-width': 2,
            'text-outline-color': '#888',
            'width': 100,
            'height': 40,
            'shape': 'square'
        })
        .selector('edge')
        .css({
            'content': 'data(name)',
            'width': 4,
            'line-color': '#888',
            'target-arrow-color': '#888',
            'source-arrow-color': '#888',
            'target-arrow-shape': 'triangle'
        })
        .selector(':selected')
        .css({
            'background-color': 'black',
            'line-color': 'black',
            'target-arrow-color': 'black',
            'source-arrow-color': 'black',
            'text-outline-color': 'black'
        })
        .selector('#cy')
        .css({
            'background-opacity': 0,
            'border-width': 1,
            'border-color': '#aaa',
            'border-opacity': 0.5,
            'font-size': 50,
            'padding-top': 10,
            'padding-left': 10,
            'padding-bottom': 10,
            'padding-right': 40
        }),

    elements: {
        nodes: [
            {
                data: {id: 'el1', name: 'Element1'},
                position: {x: 0, y: 0}
            },

            {
                data: {id: 'el2', name: 'Element2'},
                position: {x: 0, y: 150}
            },

            {
                data: {id: 'el3', name: 'Element3'},
                position: {x: -150, y: 150}
            }
        ],
        edges: [
            {data: {source: 'el1', target: 'el2'}},
            {data: {source: 'el2', target: 'el3'}},
            {data: {source: 'el1', target: 'el3'}},
        ]
    },

    layout: {
        name: 'preset'
    }
});


cy.on('tap', 'node', function (evt) {
    var node = evt.target;
    console.log(node.id());
});

function save() {
    let data = cy.json();
    console.log(data);

    $.ajax({
        type: 'POST',
        url: '/ajax/save',
        data: {
            "data": JSON.stringify(data),
            "csrfmiddlewaretoken": csrf_token
        },
        success: function (response) {
            console.log(response);
        }
    });

}