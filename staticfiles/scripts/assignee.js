function addAssignee() {
    // Get the total number of forms.
    const totalForms = document.getElementById('id_assignee_set-TOTAL_FORMS')
    const oldCount = Number(totalForms.value)
    const newCount = oldCount + 1
    totalForms.value = String(newCount)
    // Clone the last row in the table.
    const newRow = document.querySelector('tbody tr:last-child').cloneNode(true)
    // Prepare the new row.
    let oldText = "assignee_set-" + String(oldCount - 1)
    let newText = "assignee_set-" + String(newCount - 1)
    newRow.querySelectorAll('input, select').forEach(function (element) {
        // Reset the value of the element.
        element.value = (element.tagName.toLowerCase() === 'select') ? '' : 0
        // Increment the number in the "id=" and "name=" part of the elements.
        // e.g. "assignee_set-1-id" becomes "assignee_set-2-id"
        element.id = element.id.replace(oldText, newText)
        element.name = element.name.replace(oldText, newText)
    })
    // Append the cloned row to the table.
    document.querySelector('tbody').appendChild(newRow)
    // Delete the ID field of the assignee as this is a new assignee (so Django will create the ID).
    document.getElementById("id_assignee_set-" + String(newCount - 1) + "-id").remove()
}

function removeAssignee(button) {
    // Check the hidden checkbox.
    const checkbox = button.previousElementSibling.querySelector('input[type="checkbox"]')
    checkbox.checked = true
    // Disable entering of input and fade the row (cannot use disabled as that doesn't POST).
    const row = button.closest('tr')
    row.querySelectorAll('input').forEach(function (element) {
        element.readOnly = true
        element.style.backgroundColor = 'white';
    })
    row.querySelectorAll('select').forEach(function (element) {
        element.style.pointerEvents = 'none'
    })
    row.style.opacity = 0.5
}