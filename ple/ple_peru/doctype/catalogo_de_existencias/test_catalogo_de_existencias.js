/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Catalogo de Existencias", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	frappe.run_serially([
		// insert a new Catalogo de Existencias
		() => frappe.tests.make('Catalogo de Existencias', [
			// values to be set
			{key: 'value'}
		]),
		() => {
			assert.equal(cur_frm.doc.key, 'value');
		},
		() => done()
	]);

});
