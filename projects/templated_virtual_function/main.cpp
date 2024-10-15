#include <fmt/format.h>
#include <memory>
#include <vector>

class Base {
public:
  virtual void OnEvent(int a) = 0;
  virtual ~Base() = default;
};

class OrderBook {
  double last_price;
  std::vector<std::shared_ptr<Base>> listeners;

public:
  void SetLastPrice(double price) { last_price = price; }
  double GetLastPrice() { return last_price; }

  void AddListener(std::shared_ptr<Base> listener) {
    listeners.push_back(listener);
  }

  void OnEvent(int a) {
    for (auto &listener : listeners) {
      listener->OnEvent(a);
    }
  }

  void ClearListeners() { listeners.clear(); }
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

  ob->AddListener(std::make_shared<A<OrderBook>>(ob));
  ob->AddListener(std::make_shared<B<OrderBook>>(ob));

  ob->OnEvent(1);

  ob->ClearListeners();
  fmt::println("Done");
}
