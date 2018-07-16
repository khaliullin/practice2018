function getColor(value) {
    value /= 100;
    var hue = ((value) * 90).toString(10);
    return ["hsl(", hue, ",90%,35%)"].join("");
}


let cy = cytoscape({
    container: document.getElementById('cy'),
    style: cytoscape.stylesheet()
        .selector('node')
        .css({
            'content': 'data(name)',
            'text-valign': 'center',
            'background-color': '#888',
            'color': 'white',
            'text-outline-width': 2,
            'border-opacity': 0.5,
            'text-outline-color': '#888',
            'width': 100,
            'height': 40,
            'shape': 'square',
            'border-color': 'data(color)',
            'border-width': '5px'
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
            'background-color': '#515151',
            'line-color': '#515151',
            'target-arrow-color': 'black',
            'source-arrow-color': 'black',
            'text-outline-color': '#515151'
        }),
    elements: {
        nodes: [
            {
                data: {id: 'el1', name: 'Hello', description: "Some description", progress: 0, color: "white"},
                position: {x: 0, y: 0},
                params: 0
            },
            {
                data: {id: 'el2', name: 'Element2', description: "Some description", progress: 0, color: "white"},
                position: {x: 0, y: 150},
            },
            {
                data: {id: 'el3', name: 'Element3', description: "Some description", progress: 0, color: "white"},
                position: {x: -150, y: 150},
            }
        ],
        edges: [
            // {data: {source: 'el1', target: 'el2'}},
            // {data: /{source: 'el2', target: 'el3'}},
        ]
    },
    layout: {
        name: 'preset'
    }
});


// Get NODE by tap
cy.on('tap', 'node', function (evt) {
    var node = evt.target;
    if (tipp)
        tipp.hide();
    console.log(node);
    prepareEdit(node);
});

// get EDGE by tap
cy.on('tap', 'edge', function (evt) {
    let edge = evt.target;
    console.log(edge.id());
});

// Hide info block
cy.on('tap', function (evt) {
    if (!evt.target.id)
        $('#node_info').hide('fast');
});

//Reverse EDGE
cy.on('cxttapend', 'edge', function (evt) {
    let edge = evt.target;
    reverseEdge(edge);
});

function reverseEdge(edge) {
    source_id = edge._private.data.source;
    target_id = edge._private.data.target;
    let id = edge.id();
    edge.remove();
    cy.add({
        group: "edges",
        data: {id: id, source: target_id, target: source_id}
    });
    saveModel(id);
}

// Create new node
cy.on('cxttapend', function (e) {
    createNode(e);
});

function createNode(e) {
    if (!e.target.id) {
        let x = e.position.x;
        let y = e.position.y;

        console.log(x);
        console.log(y);

        let id = 'id' + Math.abs(parseInt(x, 10)) + '_' + Math.abs(parseInt(y, 10));

        let new_node = {
            group: "nodes",
            data: {id: id, name: "New", description: "", progress: 0, color: "white"},
            position: {x: x, y: y},
            selected: true
        };
        cy.add(new_node);
        console.log(new_node);

        let node = cy.$('#' + id);
        prepareEdit(node);

        saveModel(id);
    }
}


// Keyboard listener
$(document).on('keydown', function (event) {
    if (!$(event.target).is('input')) {
        // event.preventDefault();

        // delete selected item
        if (event.which === 8) {
            if (event.target.tagName.toUpperCase() !== 'TEXTAREA' && event.target.tagName.toUpperCase() !== 'INPUT') {
                removeSelected();
            }
        }

        // Connect nodes
        if (event.which === 13) {
            merge();
        }
    }
});

function removeSelected() {
    selected = cy.$(':selected');
    if (selected) {
        selected.remove();
    }

    sendRemove(selected);
}

function merge() {
    selected = cy.$('node:selected').jsons();
    console.log(selected);

    for (let i = 0; i < selected.length; i++) {
        for (let j = i; j < selected.length; j++) {
            let source_id = selected[i].data.id;
            let target_id = selected[j].data.id;
            let id = source_id + '_' + target_id;
            if (source_id !== target_id) {
                cy.add({
                    group: "edges",
                    data: {id: id, source: source_id, target: target_id}
                });
                saveModel(id);
            }
        }
    }
}

// Fill node_info block with data
function prepareEdit(node) {
    $('#title').val(node.data().name);
    $('#id').val(node.id());
    $('#description').val(node.data('description'));
    $('#progress').val(node.data('progress'));
    $('#node_info').show('fast');
}

// Rename
// keyup красиво, но порождает много запросов на сервер
$('#title').bind('change', function () {
    let id = $('#id').val();
    cy.$('#' + id).data('name', $(this).val());

    saveModel(id);
});

// Change description
$('#description').bind('change', function () {
    let id = $('#id').val();
    cy.$('#' + id).data('description', $(this).val());

    saveModel(id);
});

// Change progress
$('#progress').bind('focusout', function () {
    let id = $('#id').val();
    if ($(this).val() <= 100) {
        cy.$('#' + id).data('progress', $(this).val());
        cy.$('#' + id).data('color', getColor($(this).val()));
    }
    saveModel(id);
});


// ZOOM
cy.maxZoom(3);
cy.minZoom(0.5);

function zoomDefault() {
    cy.zoom(1);
}

function saveModel(id) {
    let data = cy.$('#' + id).json();
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


function sendRemove(elements) {
    let to_delete = [];
    $.each(elements, function (ind, el) {

        to_delete.push({
            id: el.id(),
            group: el.group()
        });
    });

    $.ajax({
        type: 'POST',
        url: '/ajax/delete',
        data: {
            "data": JSON.stringify(to_delete),
            "csrfmiddlewaretoken": csrf_token
        },
        success: function (response) {
            console.log(response);
        }
    });


}


// Send all data to server (deprecated)
function save() {
    let data = cy.json();
    console.log(data);

    $.ajax({
        type: 'POST',
        url: '/ajax/save-all',
        data: {
            "data": JSON.stringify(data),
            "csrfmiddlewaretoken": csrf_token
        },
        success: function (response) {
            cy.json(response);
            console.log(response);
        }
    });
}


// Catching NODE MOVE event
grab = false;
position_x = undefined;
position_y = undefined;
cy.on('grab', 'node', function (event) {
    hideTipp();
    position_x = event.position.x;
    position_y = event.position.y;
    grab = true;
});
cy.on('tapend', function (event) {
    if (grab)
        if (position_x !== event.position.x || position_y !== event.position.y) {
            position_x = event.position.x;
            position_y = event.position.y;
            let node = event.target;
            saveModel(node.id());
        }
    grab = false
});


// Description tippy
tipp = undefined;
var makeTippy = function (node, text) {
    return tippy(node.popperRef(), {
        html: (function () {
            var div = document.createElement('div');
            div.innerHTML = text;
            return div;
        })(),
        trigger: 'manual',
        arrow: true,
        size: 'large',
        placement: 'bottom',
        hideOnClick: false,
        multiple: true,
        sticky: true
    }).tooltips[0];
};

cy.on('tapdragover', 'node', function (e) {
    let description = e.target.data('description');
    if (description) {
        tipp = makeTippy(e.target, e.target.data('description'));
        tipp.show();
    }
});

cy.on('tapdragout', 'node', function (e) {
    hideTipp();
});

function hideTipp() {
    if (tipp)
        tipp.hide();
}


// Get user data from server
$(document).ready(function () {
    $.ajax({
        type: 'GET',
        url: '/ajax/retrieve',
        success: function (response) {
            console.log(response);
            cy.json(response);
            cy.zoom(1);
        }
    });
});

