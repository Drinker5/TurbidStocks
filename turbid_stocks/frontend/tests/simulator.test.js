import Simulator from '../src/plugins/simulator'

test('should_work', () => {
    const simulator = new Simulator()
    expect(simulator).not.toBeNull()
})

test('empty', () => {
    const simulator = new Simulator()
    expect(simulator.commissionTotal).toBe(0)
    expect(simulator.profit).toBe(0)
    expect(simulator.performance).toBe(0)
    expect(simulator.operations.length).toBe(0)
})

test('buy_work', () => {
    const simulator = new Simulator()
        .setBrokerCommission(0)
        .setStartMoney(100)
        .setLotSize(1)

    const date = new Date(2000, 10, 10)
    simulator.buy(date, 100)
    expect(simulator.operations.length).toBe(1)

    const op = simulator.operations[0]
    const expectOp = {
        time: date,
        type: "buy",
        count: 1,
        price: 100,
        commission: 0,
        value: 100,
        change: -100,
    }

    expect(op).toEqual(expectOp)
})

test('sell_work', () => {
    const simulator = new Simulator()
        .setBrokerCommission(0)
        .setStartMoney(100)
        .setLotSize(1)

    const date = new Date(2000, 10, 10)
    const date2 = new Date(2000, 10, 11)
    simulator.buy(date, 100)
    simulator.sell(date2, 100)
    expect(simulator.operations.length).toBe(2)

    const op = simulator.operations[1]
    const expectOp = {
        time: date2,
        type: "sell",
        count: 1,
        price: 100,
        commission: 0,
        value: 100,
        change: 100,
    }

    expect(op).toEqual(expectOp)
})


test('comission_work', () => {
    const simulator = new Simulator()
        .setBrokerCommission(3.5)
        .setStartMoney(100)
        .setLotSize(1)

    const date = new Date(2000, 10, 10)
    simulator.buy(date, 50)
    const op = simulator.operations[0]
    const expectOp = {
        time: date,
        type: "buy",
        count: 1,
        price: 50,
        commission: 1.75,
        value: 98.25,
        change: -51.75,
    }

    simulator.sell(date, 50)
    const op2 = simulator.operations[1]
    const expectOp2 = {
        time: date,
        type: "sell",
        count: 1,
        price: 50,
        commission: 1.75,
        value: 96.5,
        change: 48.25,
    }

    expect(op2).toEqual(expectOp2)
})