#include <fmt/format.h>
#include <memory>
#include <vector>

class OrderBook {
  double last_price;

public:
  void SetLastPrice(double price) { last_price = price; }
  double GetLastPrice() { return last_price; }
};

class Base {
public:
  virtual void OnEvent(int a) = 0;
  virtual ~Base() = default;
};

template <typename T> class A : public Base {
  std::shared_ptr<T> t;

public:
  void OnEvent(int a) override {
    fmt::println("A::OnEvent {}", a + t->GetLastPrice());
  }
  A(std::shared_ptr<T> ob) : t(ob) {}

  ~A() override = default;
};

template <typename T> class B : public Base {
  std::shared_ptr<T> t;

public:
  B(std::shared_ptr<T> ob) : t(ob) {}
  void OnEvent(int a) override {
    fmt::println("B::OnEvent {}", a + t->GetLastPrice());
  }
  ~B() override = default;
};

int main() {
  auto ob = std::make_shared<OrderBook>();
  ob->SetLastPrice(100);

  auto a = std::make_unique<A<OrderBook>>(ob);
  auto b = std::make_unique<B<OrderBook>>(ob);

  std::vector<std::unique_ptr<Base>> vec;
  vec.push_back(std::move(a));
  vec.push_back(std::move(b));

  for (auto &ptr : vec) {
    ptr->OnEvent(1);
  }

  fmt::println("Done");
}
