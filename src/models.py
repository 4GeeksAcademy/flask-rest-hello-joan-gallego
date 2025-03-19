from flask import Flask, request, jsonify

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = [
            {"id": self._generate_id(), "first_name": "John", "last_name": "Jackson", "age": 33, "lucky_numbers": [7, 13, 22]},
            {"id": self._generate_id(), "first_name": "Jane", "last_name": "Jackson", "age": 35, "lucky_numbers": [10, 14, 3]},
            {"id": self._generate_id(), "first_name": "Jimmy", "last_name": "Jackson", "age": 5, "lucky_numbers": [1]}
        ]

    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        member["id"] = self._generate_id()
        member["last_name"] = self.last_name
        self._members.append(member)
        return member

    def delete_member(self, id):
        for member in self._members:
            if member["id"] == id:
                self._members.remove(member)
                return True
        return False

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def get_all_members(self):
        return self._members

app = Flask(__name__)
jackson_family = FamilyStructure("Jackson")

@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(jackson_family.get_all_members()), 200

@app.route("/member/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404

@app.route("/member", methods=["POST"])
def add_member():
    data = request.get_json()
    if not data or "first_name" not in data or "age" not in data or "lucky_numbers" not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_member = jackson_family.add_member(data)
    return jsonify(new_member), 200

@app.route("/member/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    if jackson_family.delete_member(member_id):
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
