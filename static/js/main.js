let selected = undefined;

let cy = cytoscape({
    container: document.getElementById('cy'),
    style: cytoscape.stylesheet()
        .selector('node')
        .css({
            'content': 'data(name)',
            'text-valign': 'center',
            'color': 'white',
            'text-outline-width': 2,
            'border-opacity': 0.5,
            'text-outline-color': '#888',
            'width': 100,
            'height': 40,
            'shape': 'square'
        })
        .selector('edge')
        .css({
            'content': 'data(name)',
            'width': 4,
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'line-color': '#888',
            'target-arrow-color': '#888',
            'source-arrow-color': '#888',
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
                data: {id: 'el1', name: 'Element1', parent: 'core'},
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
        ]
    },

    layout: {
        name: 'preset'
    }
});


// Get NODE by tap
cy.on('tap', 'node', function (evt) {
    selected = evt.target;
    var node = evt.target;
    console.log(node);

    $('#title').val(node._private.data.name);
    $('#id').val(node.id());
});

// get EDGE by tap
cy.on('tap', 'edge', function (evt) {
    selected = evt.target;
    let edge = evt.target;
    console.log(edge.id());
});


//Reverse EDGE
cy.on('cxttapend', 'edge', function (evt) {
    let node = evt.target;
    source_id = node._private.data.source;
    target_id = node._private.data.target;
    node.remove();
    cy.add({
        group: "edges",
        data: {id: target_id + '-' + source_id, source: target_id, target: source_id}
    });
});


// Create new node
cy.on('cxttapend', function (e) {
    if (!e.target.id) {
        let x = e.position.x;
        let y = e.position.y;

        console.log(x);
        console.log(y);

        let new_node = {group: "nodes", data: {id: x + '_' + y}, position: {x: x, y: y}};

        cy.add(new_node);
        console.log(new_node);


    }
});


// Keyboard listener
$(document).on('keydown', function (event) {
    if (!$(event.target).is('input')) {
        console.log(event.which);
        event.preventDefault();

        // delete selected item
        if (event.which === 8) {
            if (selected) {
                selected.remove();
            }

        }

        if (event.which === 13) {
            merge();
        }
    }
});


// Send all data to server
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


function merge() {
    active = cy.$('node:selected').jsons();
    console.log(active);

    for (let i = 0; i < active.length; i++) {
        for (let j = i; j < active.length; j++) {
            let source_id = active[i].data.id;
            let target_id = active[j].data.id;
            if (source_id !== target_id) {
                cy.add({
                    group: "edges",
                    data: {id: source_id + '-' + target_id, source: source_id, target: target_id}
                });
            }

        }
    }
}


$('#title').change(function () {
    id = $('#id').val();
    el = cy.$('#'+ id)[0];
    console.log(id);
    console.log(el);
    el._private.data.name = $(this).val();
});