/* eslint-disable */
// rename this file from _test_[name] to test_[name] to activate
// and remove above this line

QUnit.test("test: Libro Electronico de Inventario Permanente Valorizado", function (assert) {
	let done = assert.async();

	// number of asserts
	assert.expect(1);

	frappe.run_serially([
		// insert a new Libro Electronico de Inventario Permanente Valorizado
		() => frappe.tests.make('Libro Electronico de Inventario Permanente Valorizado', [
			// values to be set
			{key: 'value'}
		]),
		() => {
			assert.equal(cur_frm.doc.key, 'value');
		},
		() => done()
	]);

});
