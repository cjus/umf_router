describe("UUID", function () {
  it("should be able to generate a valid UUID", function () {
    var uuid = UUID.generateWeakUUID();
    expect(uuid).toContain("-");
  });

  it("should contain 36 characters", function () {
    var uuid = UUID.generateWeakUUID();
    expect(uuid.length).toEqual(36);
  });

  it("should generate a unique ID when called each time", function () {
    var uuid1 = UUID.generateWeakUUID()
      , uuid2 = UUID.generateWeakUUID();
    expect(uuid1).toNotEqual(uuid2);
  });
});

