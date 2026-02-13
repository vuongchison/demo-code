#pragma once
#include <set>
#include <optional>

using namespace std;


class Variable {
    private:
        set<int> domain;
        optional<int> value;

    public:
        Variable(set<int> domain) : domain(domain), value(nullopt) {
        }
        Variable(initializer_list<int> domain) : domain(domain), value(nullopt) {
        }
        const set<int>& get_domain() const {
            return domain;
        }
        int get_value() const {
            return value.value();
        }
        void assign(int value) {
            if (domain.find(value) != domain.end()) {
                this->value = value;
            } else {
                throw invalid_argument("Value not in domain");
            }
        }
        void unassign() {
            value = nullopt;
        }
        
        bool is_assigned() const {
            return value.has_value();
        }

        bool remove_from_domain(int value) {
            return domain.erase(value);
        }

        void add_to_domain(int value) {
            domain.insert(value);
        }
};

