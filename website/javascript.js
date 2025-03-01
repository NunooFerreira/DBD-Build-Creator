document.getElementById('build-form').addEventListener('submit', function (e) {
    e.preventDefault();

    // Get form values
    const perk1 = document.getElementById('perk1').value;
    const perk2 = document.getElementById('perk2').value;
    const perk3 = document.getElementById('perk3').value;
    const perk4 = document.getElementById('perk4').value;
    const item = document.getElementById('item').value;
    const addon1 = document.getElementById('addon1').value;
    const addon2 = document.getElementById('addon2').value;
    const offering = document.getElementById('offering').value;
    const buildName = document.getElementById('build-name').value;

    // Validate inputs
    if (!perk1 || !perk2 || !perk3 || !perk4 || !item || !addon1 || !addon2 || !offering || !buildName) {
        alert('All fields are required!');
        return;
    }

    // Simulate image creation (for demonstration purposes)
    const output = document.getElementById('output');
    output.innerHTML = `Build image saved as <strong>${buildName}.png</strong>`;

    // Clear form
    document.getElementById('build-form').reset();
});