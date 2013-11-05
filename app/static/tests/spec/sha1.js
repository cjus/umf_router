describe("Sha1", function () {
  var sha1_value;

  beforeEach(function () {
    sha1_value = Sha1.hash("this is a test");
  });

  it("should be able to generate a valid hash", function () {
    expect(sha1_value).toEqual("fa26be19de6bff93f70bc2308434e4a440bbad02");
  });

  it("should have a length of 40 characters", function () {
    expect(sha1_value.length).toEqual(40);
  });

});

