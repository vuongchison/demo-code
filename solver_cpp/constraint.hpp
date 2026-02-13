#pragma once
#include <vector>
#include <memory>
#include <utility>
#include <optional>
#include "variable.hpp"

class Constraint {
    private:
        vector<shared_ptr<Variable>> variables_;

    public:
        Constraint(const vector<shared_ptr<Variable>>& vars) : variables_(vars) {}
        const vector<shared_ptr<Variable>>& get_variables() const {
            return variables_;
        }
        virtual ~Constraint() {}
        virtual bool is_satisfied() const = 0;
        virtual optional<pair<shared_ptr<Variable>, int>> propagate(shared_ptr<Variable> var, int val) = 0;
};

class NotEqualConstraint : public Constraint {
    private:
        shared_ptr<Variable> x_ = nullptr, y_ = nullptr;
    public:
        NotEqualConstraint(shared_ptr<Variable> x_, shared_ptr<Variable> y_) : Constraint({x_, y_}), x_(x_), y_(y_) {
            if (!x_ || !y_) {
                throw std::runtime_error("Variables not set in NotEqualConstraint");
            }
        }
        bool is_satisfied() const override {
            if (x_->is_assigned() && y_->is_assigned()) {
                return x_->get_value() != y_->get_value();
            }
            if (x_->is_assigned()) {
                return y_->get_domain().size() > 1 || y_->get_domain().count(x_->get_value()) == 0;
            }
            if (y_->is_assigned()) {
                return x_->get_domain().size() > 1 || x_->get_domain().count(y_->get_value()) == 0;
            }
            if (!x_->get_domain().size() || !y_->get_domain().size()) {
                return false;
            }
            set<int> t;
            for(int val_x : x_->get_domain()) {
                t.insert(val_x);
                if (t.size() > 1) return true;
            }
            for(int val_y : y_->get_domain()) {
                t.insert(val_y);
                if (t.size() > 1) return true;
            }
            return false;
        }

        optional<pair<shared_ptr<Variable>, int>> propagate(shared_ptr<Variable> var, int val) override {
            if (var != x_ && var != y_) {
                return nullopt;
            }
            if (var == x_ && !y_->is_assigned()) {
                if (y_->remove_from_domain(val)) {
                    return {make_pair(var, val)};
                }
            }
            if (var == y_ && !x_->is_assigned()) {
                if (x_->remove_from_domain(val)) {
                    return {make_pair(var, val)};
                }
            }
            return nullopt;
        }
};
