package mining;

import cartago.Artifact;
import cartago.OPERATION;

/** Observador exclusivo do teste: confere o estado, sem tomar decisoes pelo minerador. */
public class ValidationProbe extends Artifact {
    void init() {}

    @OPERATION void validateDelivery() {
        WorldModel world = WorldModel.get();
        if (world == null || world.getGoldsInDepot() != 1 || world.isCarryingGold(0)
                || world.countObjects(WorldModel.GOLD) != world.getInitialNbGolds()-1) {
            failed("A entrega nao corresponde ao estado do mundo");
            return;
        }
        System.out.println("GOLD_MINERS|WORLD_VERIFIED|deposited=1|carrying=false|conservation=ok");
    }
}
