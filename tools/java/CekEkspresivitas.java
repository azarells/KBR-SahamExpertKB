import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.util.*;
import java.io.File;
/** Cek ekspresivitas DL (OWLAPI DLExpressivityChecker).
 *  Pakai: java -cp "<jar pellet/owlapi>:tools/java" CekEkspresivitas output/SahamExpertKB_v2.owl */
public class CekEkspresivitas {
  public static void main(String[] a) throws Exception {
    OWLOntologyManager m = OWLManager.createOWLOntologyManager();
    m.addIRIMapper(new SimpleIRIMapper(IRI.create("http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl"),
                                       IRI.create(new File("output/SahamExpertKB_v2.owl"))));
    OWLOntology o = m.loadOntologyFromOntologyDocument(new File(a[0]));
    System.out.println(a[0] + "  ->  DL expressivity = "
        + new DLExpressivityChecker(o.getImportsClosure()).getDescriptionLogicName());
  }
}
