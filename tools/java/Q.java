import org.semanticweb.owlapi.apibinding.OWLManager;
import org.semanticweb.owlapi.model.*;
import org.semanticweb.owlapi.reasoner.*;
import com.clarkparsia.pellet.owlapiv3.PelletReasonerFactory;
import java.io.File; import java.util.*;
/** Q <owl> classes=A,B props=ind:prop,ind:prop */
public class Q {
  public static void main(String[] a) throws Exception {
    OWLOntologyManager m = OWLManager.createOWLOntologyManager();
    OWLOntology o = m.loadOntologyFromOntologyDocument(new File(a[0]));
    OWLReasoner r = PelletReasonerFactory.getInstance().createReasoner(o);
    OWLDataFactory df = m.getOWLDataFactory(); String ns = "http://kbr.kelompok9.id/ontologi/SahamExpertKB.owl#";
    System.out.println("CONSISTENT=" + r.isConsistent());
    for (int k = 1; k < a.length; k++) {
      String s = a[k];
      if (s.contains(":")) { String[] p = s.split(":");
        OWLNamedIndividual i = df.getOWLNamedIndividual(IRI.create(ns + p[0]));
        if (p[1].startsWith("@")) { Set<OWLNamedIndividual> v = r.getObjectPropertyValues(i, df.getOWLObjectProperty(IRI.create(ns + p[1].substring(1)))).getFlattened();
          List<String> n = new ArrayList<>(); for (OWLNamedIndividual x : v) n.add(x.getIRI().getFragment()); Collections.sort(n); System.out.println(s + " = " + n); }
        else { Set<OWLLiteral> v = r.getDataPropertyValues(i, df.getOWLDataProperty(IRI.create(ns + p[1]))); List<String> n = new ArrayList<>(); for (OWLLiteral l : v) n.add(l.getLiteral()); System.out.println(s + " = " + n); }
      } else {
        Set<OWLNamedIndividual> v = r.getInstances(df.getOWLClass(IRI.create(ns + s)), false).getFlattened();
        List<String> n = new ArrayList<>(); for (OWLNamedIndividual x : v) n.add(x.getIRI().getFragment()); Collections.sort(n);
        System.out.println(s + " (" + n.size() + ") = " + n);
      }
    }
  }
}
