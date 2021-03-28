import Simulator from '../src/plugins/simulator'

test('should_work', () => {
    var simulator = new Simulator()
    expect(simulator).not.toBeNull()
})