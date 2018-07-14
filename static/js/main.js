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
        }),
    elements: {
        nodes: [
            {
                data: {id: 'el1', name: 'Element1', description: "", progress: 0},
                position: {x: 0, y: 0}
            },
            {
                data: {id: 'el2', name: 'Element2', description: "", progress: 0},
                position: {x: 0, y: 150}
            },
            {
                data: {id: 'el3', name: 'Element3', description: "", progress: 0},
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
    var node = evt.target;
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
    let id = target_id + '_' + source_id;
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

        let new_node = {group: "nodes", data: {id: id, name: "New", description: "", progress: 0}, position: {x: x, y: y}, selected: true};
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
$('#progress').bind('change', function () {
    let id = $('#id').val();
    cy.$('#' + id).data('progress', $(this).val());

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
            id:   el.id(),
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


// let json = JSON.parse('{"elements":{"nodes":[{"data":{"id":"id140_23","name":"1","description":"1","progress":"1"},"position":{"x":-140.98167938931294,"y":-23.106870229007626},"group":"nodes","removed":false,"selected":false,"selectable":true,"locked":false,"grabbable":true,"classes":""},{"data":{"id":"id57_78","name":"3","description":"3","progress":"3"},"position":{"x":-57.4946564885496,"y":78.07786259541984},"group":"nodes","removed":false,"selected":true,"selectable":true,"locked":false,"grabbable":true,"classes":""},{"data":{"id":"id21_9","name":"2","description":"2","progress":"2"},"position":{"x":-21.714503816793876,"y":9.59541984732825},"group":"nodes","removed":false,"selected":false,"selectable":true,"locked":false,"grabbable":true,"classes":""}],"edges":[{"data":{"id":"id140_23_id21_9","source":"id140_23","target":"id21_9"},"position":{},"group":"edges","removed":false,"selected":false,"selectable":true,"locked":false,"grabbable":true,"classes":""},{"data":{"id":"id57_78_id21_9","source":"id57_78","target":"id21_9"},"position":{},"group":"edges","removed":false,"selected":false,"selectable":true,"locked":false,"grabbable":true,"classes":""}]},"style":[{"selector":"node","style":{"text-valign":"center","color":"white","text-outline-color":"#888","text-outline-width":"2px","height":"40px","width":"100px","shape":"square","border-opacity":"0.5","label":"data(name)"}},{"selector":"edge","style":{"width":"4px","line-color":"#888","curve-style":"bezier","target-arrow-shape":"triangle","source-arrow-color":"#888","target-arrow-color":"#888","label":"data(name)"}},{"selector":":selected","style":{"text-outline-color":"black","background-color":"black","line-color":"black","source-arrow-color":"black","target-arrow-color":"black"}}],"zoomingEnabled":true,"userZoomingEnabled":true,"zoom":2.5992063492063493,"minZoom":0.5,"maxZoom":3,"panningEnabled":true,"userPanningEnabled":true,"pan":{"x":552.4404761904761,"y":277.0595238095238},"boxSelectionEnabled":true,"renderer":{"name":"canvas"}}');
// cy.json(json);


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
